# Visor Urbano: Step-by-Step Developer Setup Guide

A beginner-friendly, comprehensive guide for setting up your development environment for Visor Urbano. This document helps developers get started even if they are unfamiliar with command-line tools.

---

## 🚀 Before You Start: Recommended Tools

If you don’t have command-line experience, we suggest installing the following tools:

### 1. [GitHub Desktop](https://desktop.github.com/download/)

A graphical Git client that simplifies cloning, committing, and syncing repositories. Ideal for developers not familiar with terminal-based Git commands.

### 2. [Visual Studio Code](https://code.visualstudio.com)

A powerful and lightweight code editor. Recommended for its excellent integration with extensions like GitHub Copilot, which provides AI-powered code suggestions and completions.

### 3. [Docker Desktop](https://www.docker.com/products/docker-desktop/)

Essential for running containerized backend services like the database and FastAPI server. Enables consistent development environments across machines.

### 4. [Node.js](https://nodejs.org/en/download)

Required to run the frontend using React and Vite. Includes `npm`, which is used for running scripts and installing packages.

### 5. [pnpm](https://pnpm.io/installation)

A fast and disk-efficient package manager. It replaces `npm` and `yarn`, and is essential for managing dependencies in this monorepo project.

### 6. [pgAdmin](https://www.pgadmin.org/download/)

A user-friendly GUI to manage PostgreSQL databases. Useful for exploring and debugging database tables, queries, and schemas.

---

## 📚 Step-by-Step Installation Guide

> **Step 0:** Make sure you have all the recommended tools installed (GitHub Desktop, VS Code, Docker, Node.js, pnpm, pgAdmin). Once installed, follow the steps below:

### 1. Clone the Repository

- Go to: [https://github.com/Delivery-Associates/visor-urbano](https://github.com/Delivery-Associates/visor-urbano)
- Click on **Code** > **Open with GitHub Desktop**

### 2. Use GitHub Desktop

- In the GitHub Desktop window, choose the local folder to store the project and click **Clone**

### 3. Open in Visual Studio Code

- Once cloned, click **Open in Visual Studio Code** from GitHub Desktop

### 4. Preview the README

- In VS Code, click on `README.md`, then open the Markdown preview to see the formatted documentation.

### 5. Run the Setup Script

- Open an integrated terminal in VS Code (Terminal > New Terminal), and run:

```bash
./setup.sh
```

- If you see this error: `❌ Docker is installed but not running`, it means Docker is installed but not open. Please launch **Docker Desktop**.
- If you’ve used Docker before, make sure there are no old containers, volumes, images or builds running — they might cause conflicts.\

### 5.1 Once Docker is Running

- Run the setup script again:

```bash
./setup.sh
```

- When you see this message:

```bash
Next Steps:
1. Review and update .env files with your configuration
2. Ensure your database is running (if using local setup)
3. Run 'pnpm dev' to start the development environment
```

... it means your environment is ready.

### 6. Start the Development Environment

Run the following:

```bash
pnpm dev
```

- Wait while all dependencies are installed. When it's ready, you’ll see:

```
Uvicorn running on http://0.0.0.0:8000
```

At this point, the following services are running:

- Frontend: [localhost:5173](http://localhost:5173)
- Backend: [localhost:8000](http://localhost:8000)
- PostgreSQL Database: **postgresql://visorurbano:visorurbano123456@localhost:5432/visorurbano_prod** (accessible via pgAdmin)
- Documentation Portal: [localhost:3000](http://localhost:3000)
- Swagger UI (Backend API Docs): [localhost:8000/docs](http://localhost:8000/docs)
- Redocs (Alternative API Docs): [localhost:8000/redoc](http://localhost:8000/redoc)
- Storybook (UI Components): [localhost:6006](http://localhost:6006)

### pgAdmin Configuration for Visor Urbano

This configuration comes from your `apps/backend/.env`

To connect to the PostgreSQL database using pgAdmin:

### General Tab:

- **Name**: `Visor Urbano Development`

### Connection Tab:

| Field                    | Value               |
| ------------------------ | ------------------- |
| **Host name/address**    | `localhost`         |
| **Port**                 | `5432`              |
| **Maintenance database** | `visorurbano_prod`  |
| **Username**             | `visorurbano`       |
| **Password**             | `visorurbano123456` |

### Additional Settings:

- **Kerberos authentication?** → ❌ **Disabled** (toggle OFF)
- **Save password?** → ✅ **Enabled** (toggle ON) - so you don't have to enter it every time
- **Role** → Leave empty
- **Service** → Leave empty

### Important Notes:

1. **Make sure Docker is running** before connecting
2. If you have connection issues, verify that port 5432 isn't being used by another PostgreSQL instance

### To verify it works:

Once connected, you should see:

- Database: `visorurbano_prod`
- Schema: `public`
- System tables like: `users`, `municipalities`, `procedures`, etc.

### 7. Load Mock Data

Keep the terminal running `pnpm dev` open. In a new terminal, run:

```bash
./setup-test-data.sh
```

This script loads sample data so you can explore the app without needing to enter everything manually. **Note:** This data is for development only and should never be pushed to production.

### 8. Test User Accounts

```bash
🎉 Test data setup completed successfully!

🔐 You can now log in with the following development accounts:
👑 Admin: admin@visorurbano.com / Admin12345678.
🏩 Director: director@visorurbano.com / Director12345678.
📜 Reviewer: reviewer@visorurbano.com / Reviewer12345678.
🏪 Counter: counter@visorurbano.com / Counter12345678.
👤 Citizen: citizen@visorurbano.com / Citizen12345678.
```

We recommend starting with these roles:

- **Citizen**: to test the platform as a regular user
- **Director**: to explore admin functionalities

### Common Issues

- ❌ **Old Docker containers**: If you repeat setup steps without stopping/removing old containers, things may break. Use `docker ps -a` and `docker rm -f [id]` to clean up.
- ⚡ **Browser cache**: If the frontend throws an error after reinstalling, clear your browser cache. This usually happens because the previous session’s token is invalid.

---

## 📄 Internal Documentation & URLs

### Development Environment (Once Running):

- **Frontend:** [http://localhost:5173](http://localhost:5173)
- **Backend:** [http://localhost:8000](http://localhost:8000)
- **Docs Portal:** [http://localhost:3000](http://localhost:3000)
- **Storybook (Frontend UI Documentation):** [http://localhost:6006](http://localhost:6006)
- **Swagger UI (Backend API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Redoc (Alternate Backend API Docs):** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📅 External Documentation

- [Storybook Docs](https://storybook.js.org/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/python-types/#motivation)
- [React Router Docs](https://reactrouter.com/start/declarative/installation)
- [Vite Guide](https://vite.dev/guide/)
- [Docker Manual](https://docs.docker.com/manuals/)
- [Swagger API Docs](https://swagger.io/docs/)

---

## ✨ Quick Start (Terminal Users)

```bash
# 1. Clone and enter the repository
git clone <repository-url>
cd visor-urbano

# 2. Run the setup script
./setup.sh

# 3. Start the development environment
pnpm dev

# 4. (Optional) Load test data
./setup-test-data.sh
```

If you're not using the terminal regularly, you can use GitHub Desktop to clone the project, then open the folder in VS Code and run commands from its terminal.

---

## 🧰 Tips for New Developers

- Use **GitHub Desktop** for managing Git commits and pushing code.
- Enable **GitHub Copilot** in VS Code for code suggestions and documentation generation.
- Use **pgAdmin** to inspect the database visually instead of command-line queries.
- Keep **Docker Desktop** running to avoid connectivity issues with backend services.
- All main commands are run with `pnpm`, not `npm`.

For more advanced setups or debugging instructions, refer to the full [README](./README.md) in the project root.

---

Happy coding! 🚀
