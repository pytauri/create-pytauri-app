import fs from 'fs-extra'
import path from 'node:path'
import spawn from 'cross-spawn'
import mri from 'mri'
import {fileURLToPath} from 'node:url'
import {Liquid} from 'liquidjs';

// REF: https://github.com/vitejs/vite/blob/main/packages/create-vite/src/index.ts

// Initialize the Liquid engine
const liquid = new Liquid();

const argv = mri<{
    template?: string
    help?: boolean
    overwrite?: boolean
}>(process.argv.slice(2), {
    alias: {h: 'help', t: 'template'}, boolean: ['help', 'overwrite'], string: ['template'],
})

// prettier-ignore
const helpMessage = `\
Usage: create-pytauri [OPTION]... [DIRECTORY]

Create a new pytauri project. Uses the create-tauri CLI as base.
With no arguments, start the CLI in interactive mode.
`


async function init() {
    const projectName = "tauri-app"

    const help = argv.help
    if (help) {
        console.log(helpMessage)
        return
    }

    const child = spawn('npm', ['create', 'tauri-app@latest', 'tauri-app', '--', '--template', 'vue-ts', '--manager', 'npm', '--yes'], {
        stdio: 'inherit', // pipe output directly to current process
        shell: true       // required on Windows for commands like `npm`
    });

    const root = path.resolve(fileURLToPath(import.meta.url), '../..',)
    const templateDir = path.join(root, "template-python")

    child.on('close', (code) => {
        const dest = path.join(root, "tauri-app")
        copy(templateDir, path.join(dest, "src-tauri"))

        const base = path.join(dest, "src-tauri", "src-python")
        renameDirectory(path.join(base, "src", "pytauri_vue_starter"), path.join(base, "src", projectName))
        processTomlFile(path.join(base, "pyproject.toml"), {project_name: projectName})
    });
}


function copy(src: string, dest: string) {
    const stat = fs.statSync(src)
    if (stat.isDirectory()) {
        copyDir(src, dest)
    } else {
        fs.copyFileSync(src, dest)
    }
}

function copyDir(srcDir: string, destDir: string) {
    fs.mkdirSync(destDir, {recursive: true})
    for (const file of fs.readdirSync(srcDir)) {
        const srcFile = path.resolve(srcDir, file)
        const destFile = path.resolve(destDir, file)
        copy(srcFile, destFile)
    }
}

const renameDirectory = async (oldDir: string, newDir: string) => {
    try {
        // Ensure the old directory exists and the new directory doesn't
        if (await fs.pathExists(oldDir) && !(await fs.pathExists(newDir))) {
            // Rename the directory
            await fs.rename(oldDir, newDir);
            console.log(`Directory renamed from "${oldDir}" to "${newDir}"`);
        } else {
            console.log("Directory rename failed. Either source doesn't exist or target exists.");
        }
    } catch (err) {
        console.error('Error renaming directory:', err);
    }
};

const processTomlFile = async (filePath: string, context: any) => {
    try {
        // Use synchronous file reading
        const tomlContent = fs.readFileSync(filePath, 'utf-8');

        console.log(context);

        // Render the Liquid template with the provided context
        const rendered = await liquid.parseAndRender(tomlContent, context);

        // Save the modified file
        fs.writeFileSync(filePath, rendered, 'utf-8');
        console.log(`TOML file processed: ${filePath}`);
    } catch (err) {
        console.error('Error processing TOML file:', err);
    }
};

init().catch((e) => {
    console.error(e)
})