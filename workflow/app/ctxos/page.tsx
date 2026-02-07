"use client"

import type React from "react"
import { useState, useCallback, useRef, useEffect } from "react"
import {
    ReactFlow,
    applyNodeChanges,
    applyEdgeChanges,
    addEdge,
    Background,
    Controls,
    MiniMap,
    type Node,
    type Edge,
    type OnNodesChange,
    type OnEdgesChange,
    type OnConnect,
    type NodeTypes,
    type ReactFlowInstance,
} from "@xyflow/react"
import "@xyflow/react/dist/style.css"
import { Button } from "@/components/ui/button"
import { Play, Download, Upload, Menu, X, Package, Server, Box, Layers } from "lucide-react"

// CtxOS-specific node types
const nodeTypes: NodeTypes = {
    module: ({ data }: any) => (
        <div className="px-4 py-3 shadow-lg rounded-lg bg-gradient-to-br from-blue-500 to-blue-600 border-2 border-blue-400 min-w-[180px]">
            <div className="flex items-center gap-2 mb-1">
                <Package className="h-4 w-4 text-white" />
                <div className="font-bold text-white text-sm">{data.label}</div>
            </div>
            <div className="text-xs text-blue-100">{data.description}</div>
            {data.packages && (
                <div className="mt-2 text-xs text-blue-50 opacity-80">
                    {data.packages} packages
                </div>
            )}
        </div>
    ),
    script: ({ data }: any) => (
        <div className="px-4 py-3 shadow-lg rounded-lg bg-gradient-to-br from-purple-500 to-purple-600 border-2 border-purple-400 min-w-[180px]">
            <div className="flex items-center gap-2 mb-1">
                <Server className="h-4 w-4 text-white" />
                <div className="font-bold text-white text-sm">{data.label}</div>
            </div>
            <div className="text-xs text-purple-100">{data.description}</div>
            {data.output && (
                <div className="mt-2 text-xs text-purple-50 opacity-80">
                    → {data.output}
                </div>
            )}
        </div>
    ),
    artifact: ({ data }: any) => (
        <div className="px-4 py-3 shadow-lg rounded-lg bg-gradient-to-br from-green-500 to-green-600 border-2 border-green-400 min-w-[180px]">
            <div className="flex items-center gap-2 mb-1">
                <Box className="h-4 w-4 text-white" />
                <div className="font-bold text-white text-sm">{data.label}</div>
            </div>
            <div className="text-xs text-green-100">{data.description}</div>
            {data.format && (
                <div className="mt-2 text-xs text-green-50 opacity-80">
                    Format: {data.format}
                </div>
            )}
        </div>
    ),
    stage: ({ data }: any) => (
        <div className="px-4 py-3 shadow-lg rounded-lg bg-gradient-to-br from-orange-500 to-orange-600 border-2 border-orange-400 min-w-[200px]">
            <div className="flex items-center gap-2 mb-1">
                <Layers className="h-4 w-4 text-white" />
                <div className="font-bold text-white text-sm">{data.label}</div>
            </div>
            <div className="text-xs text-orange-100">{data.description}</div>
            {data.status && (
                <div className="mt-2 px-2 py-1 bg-orange-400/30 rounded text-xs text-white">
                    {data.status}
                </div>
            )}
        </div>
    ),
}

// CtxOS Build Pipeline Nodes
const ctxosNodes: Node[] = [
    // Stage 1: Source Modules
    {
        id: "mod-core",
        type: "module",
        position: { x: 50, y: 100 },
        data: { label: "Core Module", description: "Base system utilities", packages: "15" },
    },
    {
        id: "mod-desktop",
        type: "module",
        position: { x: 50, y: 220 },
        data: { label: "Desktop Module", description: "GNOME environment", packages: "8" },
    },
    {
        id: "mod-tools",
        type: "module",
        position: { x: 50, y: 340 },
        data: { label: "Tools Module", description: "Development tools", packages: "12" },
    },
    {
        id: "mod-software-center",
        type: "module",
        position: { x: 50, y: 460 },
        data: { label: "Software Center", description: "Package manager UI", packages: "1" },
    },

    // Stage 2: Build Scripts
    {
        id: "script-build-debs",
        type: "script",
        position: { x: 350, y: 100 },
        data: { label: "build-debs.sh", description: "Build meta-packages", output: ".deb files" },
    },
    {
        id: "script-software-center",
        type: "script",
        position: { x: 350, y: 460 },
        data: { label: "make build-deb", description: "Build Software Center", output: "software-center.deb" },
    },

    // Stage 3: Repository Management
    {
        id: "script-repo",
        type: "script",
        position: { x: 650, y: 200 },
        data: { label: "manage-repo.sh", description: "Aptly repository", output: "APT repo" },
    },

    // Stage 4: Pipeline Orchestration
    {
        id: "stage-pipeline",
        type: "stage",
        position: { x: 950, y: 250 },
        data: { label: "Pipeline Master", description: "Orchestrate full build", status: "Running" },
    },

    // Stage 5: Artifacts
    {
        id: "artifact-docker",
        type: "artifact",
        position: { x: 1300, y: 100 },
        data: { label: "Docker Image", description: "ctxos-base:latest", format: "OCI" },
    },
    {
        id: "artifact-iso",
        type: "artifact",
        position: { x: 1300, y: 250 },
        data: { label: "Live ISO", description: "Bootable image", format: "ISO 9660" },
    },
    {
        id: "artifact-repo",
        type: "artifact",
        position: { x: 1300, y: 400 },
        data: { label: "APT Repository", description: "Published packages", format: "Aptly" },
    },

    // Stage 6: Validation
    {
        id: "script-validate",
        type: "script",
        position: { x: 1650, y: 250 },
        data: { label: "validate-artifacts.sh", description: "Health checks", output: "Report" },
    },

    // Stage 7: Release
    {
        id: "stage-release",
        type: "stage",
        position: { x: 1950, y: 250 },
        data: { label: "Release", description: "Tag & publish", status: "Ready" },
    },
]

const ctxosEdges: Edge[] = [
    // Modules to build scripts
    { id: "e1", source: "mod-core", target: "script-build-debs" },
    { id: "e2", source: "mod-desktop", target: "script-build-debs" },
    { id: "e3", source: "mod-tools", target: "script-build-debs" },
    { id: "e4", source: "mod-software-center", target: "script-software-center" },

    // Build scripts to repo
    { id: "e5", source: "script-build-debs", target: "script-repo" },
    { id: "e6", source: "script-software-center", target: "script-repo" },

    // Repo to pipeline
    { id: "e7", source: "script-repo", target: "stage-pipeline" },

    // Pipeline to artifacts
    { id: "e8", source: "stage-pipeline", target: "artifact-docker" },
    { id: "e9", source: "stage-pipeline", target: "artifact-iso" },
    { id: "e10", source: "stage-pipeline", target: "artifact-repo" },

    // Artifacts to validation
    { id: "e11", source: "artifact-docker", target: "script-validate" },
    { id: "e12", source: "artifact-iso", target: "script-validate" },
    { id: "e13", source: "artifact-repo", target: "script-validate" },

    // Validation to release
    { id: "e14", source: "script-validate", target: "stage-release" },
]

export default function CtxOSBuilder() {
    const [nodes, setNodes] = useState<Node[]>(ctxosNodes)
    const [edges, setEdges] = useState<Edge[]>(ctxosEdges)
    const [reactFlowInstance, setReactFlowInstance] = useState<ReactFlowInstance | null>(null)
    const reactFlowWrapper = useRef<HTMLDivElement>(null)
    const fileInputRef = useRef<HTMLInputElement>(null)
    const [isPaletteOpen, setIsPaletteOpen] = useState(false)

    const onNodesChange: OnNodesChange = useCallback((changes) => setNodes((nds) => applyNodeChanges(changes, nds)), [])
    const onEdgesChange: OnEdgesChange = useCallback((changes) => setEdges((eds) => applyEdgeChanges(changes, eds)), [])
    const onConnect: OnConnect = useCallback((params) => setEdges((eds) => addEdge(params, eds)), [])

    const handleExportWorkflow = useCallback(() => {
        const workflow = { nodes, edges }
        const blob = new Blob([JSON.stringify(workflow, null, 2)], { type: "application/json" })
        const url = URL.createObjectURL(blob)
        const a = document.createElement("a")
        a.href = url
        a.download = `ctxos-build-map-${new Date().toISOString().slice(0, 10)}.json`
        document.body.appendChild(a)
        a.click()
        document.body.removeChild(a)
        URL.revokeObjectURL(url)
    }, [nodes, edges])

    const handleImportWorkflow = useCallback(
        (event: React.ChangeEvent<HTMLInputElement>) => {
            const file = event.target.files?.[0]
            if (!file) return

            const reader = new FileReader()
            reader.onload = (e) => {
                try {
                    const content = e.target?.result as string
                    const workflow = JSON.parse(content)

                    if (workflow.nodes && workflow.edges) {
                        setNodes(workflow.nodes)
                        setEdges(workflow.edges)
                    } else {
                        alert("Invalid workflow file format")
                    }
                } catch (error) {
                    console.error("Failed to import workflow:", error)
                    alert("Failed to import workflow. Please check the file format.")
                }
            }
            reader.readAsText(file)

            if (fileInputRef.current) {
                fileInputRef.current.value = ""
            }
        },
        [],
    )

    return (
        <div className="flex h-screen w-full flex-col bg-background">
            {/* Header */}
            <header className="flex flex-col gap-3 border-b border-border bg-card px-4 py-3 md:flex-row md:items-center md:justify-between md:px-6 md:py-4">
                <div className="flex items-center gap-3">
                    <Button
                        variant="ghost"
                        size="icon"
                        className="md:hidden"
                        onClick={() => setIsPaletteOpen(!isPaletteOpen)}
                        aria-label="Toggle menu"
                    >
                        {isPaletteOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
                    </Button>
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
                        <Layers className="h-5 w-5 text-white" />
                    </div>
                    <div>
                        <h1 className="text-lg font-semibold text-foreground md:text-xl">CtxOS Build Pipeline</h1>
                        <p className="text-xs text-muted-foreground md:text-sm">Distribution Build Flow Visualizer</p>
                    </div>
                </div>
                <div className="flex flex-wrap items-center gap-2 md:gap-3">
                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".json"
                        onChange={handleImportWorkflow}
                        className="hidden"
                        aria-label="Import workflow"
                    />
                    <Button variant="outline" size="sm" onClick={() => fileInputRef.current?.click()}>
                        <Upload className="mr-2 h-4 w-4" />
                        Import
                    </Button>
                    <Button variant="outline" size="sm" onClick={handleExportWorkflow}>
                        <Download className="mr-2 h-4 w-4" />
                        Export
                    </Button>
                    <Button size="sm" className="bg-primary hover:bg-primary/90">
                        <Play className="mr-2 h-4 w-4" />
                        Execute Build
                    </Button>
                </div>
            </header>

            {/* Main Content */}
            <div className="relative flex flex-1 overflow-hidden">
                {/* React Flow Canvas */}
                <div className="flex-1" ref={reactFlowWrapper}>
                    <ReactFlow
                        nodes={nodes}
                        edges={edges}
                        onNodesChange={onNodesChange}
                        onEdgesChange={onEdgesChange}
                        onConnect={onConnect}
                        onInit={setReactFlowInstance}
                        nodeTypes={nodeTypes}
                        fitView
                        className="bg-background"
                    >
                        <Background className="bg-background" gap={16} size={1} />
                        <Controls />
                        <MiniMap
                            pannable
                            zoomable
                            className="bg-card border border-border"
                            maskColor="rgb(0, 0, 0, 0.6)"
                            nodeColor={(node) => {
                                switch (node.type) {
                                    case "module":
                                        return "oklch(0.60 0.25 240)"
                                    case "script":
                                        return "oklch(0.60 0.25 280)"
                                    case "artifact":
                                        return "oklch(0.65 0.25 140)"
                                    case "stage":
                                        return "oklch(0.65 0.25 40)"
                                    default:
                                        return "oklch(0.65 0.25 265)"
                                }
                            }}
                        />
                    </ReactFlow>
                </div>
            </div>
        </div>
    )
}
