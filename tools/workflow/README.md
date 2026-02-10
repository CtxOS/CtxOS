# CtxOS Workflow Visualizer

A Next.js-based visual workflow builder and build pipeline visualizer for the CtxOS distribution project.

## Features

### 1. **AI Agent Builder** (`/`)
- Visual workflow designer for AI SDK
- Drag-and-drop node-based interface
- Support for multiple AI model types (text, embedding, image generation, audio)
- Code export functionality
- Workflow import/export

### 2. **CtxOS Build Pipeline** (`/ctxos`)
- Visualizes the complete CtxOS distribution build flow
- Shows module dependencies and build stages
- Tracks artifacts (Docker images, ISOs, APT repositories)
- Interactive pipeline exploration

## Node Types

### CtxOS Pipeline Nodes

- **Module**: Source code modules (core, desktop, tools, software-center)
- **Script**: Build scripts (build-debs.sh, manage-repo.sh, etc.)
- **Artifact**: Build outputs (Docker images, ISOs, APT repos)
- **Stage**: Pipeline stages (orchestration, validation, release)

## Getting Started

### Prerequisites

- Node.js 18+ or Bun
- pnpm (recommended) or npm

### Installation

```bash
cd workflow
pnpm install
```

### Development

```bash
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to view the AI Agent Builder.

Open [http://localhost:3000/ctxos](http://localhost:3000/ctxos) to view the CtxOS Build Pipeline.

### Build

```bash
pnpm build
pnpm start
```

## Project Structure

```
workflow/
├── app/
│   ├── page.tsx              # AI Agent Builder (main page)
│   ├── ctxos/
│   │   └── page.tsx          # CtxOS Build Pipeline Visualizer
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Global styles
├── components/
│   ├── nodes/                # Custom node components
│   ├── ui/                   # shadcn/ui components
│   ├── node-palette.tsx      # Node selection palette
│   ├── node-config-panel.tsx # Node configuration panel
│   ├── code-export-dialog.tsx # Code export dialog
│   └── execution-panel.tsx   # Workflow execution panel
├── lib/
│   └── utils.ts              # Utility functions
└── public/                   # Static assets
```

## CtxOS Build Pipeline Flow

The CtxOS build pipeline follows this flow:

1. **Source Modules** → Meta-packages are defined in `modules/`
2. **Build Scripts** → `build-debs.sh` compiles .deb packages
3. **Repository Management** → `manage-repo.sh` publishes to Aptly
4. **Pipeline Orchestration** → `pipeline-master.sh` coordinates the build
5. **Artifacts** → Docker images, Live ISOs, APT repositories
6. **Validation** → `validate-artifacts.sh` performs health checks
7. **Release** → Git tagging and publication

## Technologies

- **Next.js 15** - React framework
- **React Flow** - Node-based UI library
- **Tailwind CSS 4** - Styling
- **shadcn/ui** - UI components
- **TypeScript** - Type safety
- **Vercel AI SDK** - AI integration (for agent builder)

## Integration with CtxOS

This workflow visualizer is part of the CtxOS project and provides:

- **Documentation**: Visual representation of the build process
- **Debugging**: Identify bottlenecks in the pipeline
- **Planning**: Design new build stages and dependencies
- **Monitoring**: Track build progress in real-time (future feature)

## Customization

### Adding New Node Types

1. Create a new node component in `components/nodes/`
2. Register it in the `nodeTypes` object
3. Add default data in `getDefaultNodeData()`
4. Update the node palette

### Extending the CtxOS Pipeline

Edit `/app/ctxos/page.tsx` to:
- Add new modules, scripts, or artifacts
- Modify the build flow
- Customize node appearance

## License

MIT - Part of the CtxOS project

## Contributing

This is a development tool for the CtxOS distribution. Contributions should align with the overall CtxOS architecture.
