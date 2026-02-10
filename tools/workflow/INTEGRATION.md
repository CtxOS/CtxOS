# CtxOS Workflow Integration Guide

This document explains how the workflow visualizer integrates with the CtxOS distribution project.

## Overview

The `workflow/` directory contains a Next.js application that provides visual tools for understanding and managing the CtxOS build pipeline.

## Setup

### 1. Install Dependencies

```bash
cd workflow
pnpm install
# or
npm install
```

### 2. Run Development Server

```bash
pnpm dev
```

Visit:
- http://localhost:3000 - AI Agent Builder (general purpose)
- http://localhost:3000/ctxos - CtxOS Build Pipeline Visualizer

## CtxOS Build Pipeline Visualization

The `/ctxos` route provides an interactive visualization of the complete CtxOS build process:

### Pipeline Stages

1. **Source Modules** (Blue nodes)
   - `modules/core` - Base system utilities
   - `modules/desktop` - GNOME desktop environment
   - `modules/tools` - Development tools
   - `software-center` - Package manager UI

2. **Build Scripts** (Purple nodes)
   - `packaging/build-debs.sh` - Builds meta-packages
   - `software-center/Makefile` - Builds Software Center
   - `packaging/repo/manage-repo.sh` - Manages APT repository

3. **Pipeline Orchestration** (Orange nodes)
   - `scripts/pipeline-master.sh` - Master build coordinator
   - Coordinates all build stages
   - Manages dependencies

4. **Build Artifacts** (Green nodes)
   - Docker Image: `ctxos-base:latest`
   - Live ISO: Bootable installation media
   - APT Repository: Published package repository

5. **Validation & Release** (Orange/Purple nodes)
   - `scripts/validate-artifacts.sh` - Health checks
   - Git tagging and publication

### Node Types

#### Module Node
Represents source code modules that contain:
- Package definitions
- Installation scripts
- Configuration files

#### Script Node
Represents build scripts that:
- Transform modules into packages
- Manage repositories
- Coordinate builds

#### Artifact Node
Represents build outputs:
- Binary packages (.deb)
- Container images
- ISO images
- APT repositories

#### Stage Node
Represents pipeline stages:
- Orchestration points
- Validation gates
- Release triggers

## Customizing the Pipeline View

### Adding New Modules

Edit `workflow/app/ctxos/page.tsx`:

```typescript
{
  id: "mod-your-module",
  type: "module",
  position: { x: 50, y: 580 },
  data: {
    label: "Your Module",
    description: "Module description",
    packages: "5"
  },
}
```

### Adding New Build Scripts

```typescript
{
  id: "script-your-script",
  type: "script",
  position: { x: 350, y: 580 },
  data: {
    label: "your-script.sh",
    description: "Script purpose",
    output: "Output type"
  },
}
```

### Connecting Nodes

```typescript
{
  id: "e-new",
  source: "mod-your-module",
  target: "script-your-script"
}
```

## Integration with CI/CD

The workflow visualizer can be used to:

1. **Document the build process** - Share with team members
2. **Debug build failures** - Identify which stage failed
3. **Plan new features** - Design new modules and dependencies
4. **Monitor builds** - (Future) Real-time build status

### GitHub Actions Integration

The pipeline visualization maps directly to GitHub Actions workflows:

- `.github/workflows/ci.yml` - Continuous integration (lint, build)
- `.github/workflows/software-center.yml` - Software Center build
- `.github/workflows/production-pipeline.yml` - Full release pipeline

## Exporting Pipeline Diagrams

### JSON Export
Click "Export" to save the current pipeline as JSON. This can be:
- Versioned in git
- Shared with team members
- Imported later for reference

### Screenshot/PDF Export
Use browser tools to capture the visualization:
1. Open the pipeline view
2. Use browser print (Cmd/Ctrl + P)
3. Save as PDF

## Future Enhancements

### Planned Features

1. **Real-time Build Status**
   - Connect to GitHub Actions API
   - Show live build progress
   - Highlight failed stages

2. **Interactive Execution**
   - Trigger builds from the UI
   - View logs inline
   - Retry failed stages

3. **Dependency Analysis**
   - Show package dependencies
   - Identify circular dependencies
   - Suggest optimizations

4. **Performance Metrics**
   - Build time tracking
   - Resource usage
   - Bottleneck identification

## Development

### Project Structure

```
workflow/
├── app/
│   ├── page.tsx           # AI Agent Builder
│   ├── ctxos/
│   │   └── page.tsx       # CtxOS Pipeline Visualizer
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── ui/                # shadcn/ui components
│   └── ...
├── lib/
│   └── utils.ts
└── public/
```

### Adding New Features

1. Create new route in `app/`
2. Add custom node types if needed
3. Update README with documentation
4. Test with `pnpm dev`

### Styling

The visualizer uses:
- Tailwind CSS 4 for styling
- shadcn/ui for components
- Custom gradients for node types

### TypeScript

All code is fully typed. Key types:
- `Node` - React Flow node
- `Edge` - React Flow edge
- `NodeTypes` - Custom node type registry

## Deployment

### Production Build

```bash
cd workflow
pnpm build
pnpm start
```

### Docker Deployment

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY workflow/ .
RUN npm install -g pnpm && pnpm install
RUN pnpm build
CMD ["pnpm", "start"]
```

### Static Export

For static hosting:

```bash
# Update next.config.mjs
export default {
  output: 'export',
}

# Build
pnpm build
```

## Contributing

When adding new CtxOS modules or scripts:

1. Update the pipeline visualization
2. Add documentation to this guide
3. Export the updated pipeline JSON
4. Commit changes to git

## Support

For questions about the workflow visualizer:
- Check the README.md in `workflow/`
- Review the React Flow documentation
- Consult the CtxOS architecture docs

## License

MIT - Part of the CtxOS project
