import {defineBuildConfig} from 'unbuild'


export default defineBuildConfig({
    entries: ['src/index'],
    clean: true,
    rollup: {
        inlineDependencies: true,
        esbuild: {
            target: 'node18',
            minify: true,
        },
    },
    hooks: {
        'rollup:options'(_ctx, options) {
            options.plugins = [
                options.plugins,
            ]
        },
    },
})

