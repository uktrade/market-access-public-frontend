'use strict';

const production = ((process.env.NODE_ENV || 'dev').trim().toLowerCase() === 'production');
const
    gulp = require('gulp'),
    concat = require('gulp-concat'),
    gulpif = require('gulp-if'),
    babel = require('gulp-babel'),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify');

const sass = require('gulp-sass')(require('sass'));

// NOTES
// Useful tips for uglifying - https://stackoverflow.com/questions/24591854/using-gulp-to-concatenate-and-uglify-files

// Source paths
const
    assetsSrcPath = 'apps/static/src/',
    scssEntryFile = `${assetsSrcPath}scss/index.scss`,
    govukAssets = 'node_modules/govuk-frontend/govuk/assets/';

// Build / Distribution paths
const
    assetsBuildPath = 'apps/static/dist/',
    cssBuildPath = `${assetsBuildPath}css`,
    cssBuildFileName = 'main.css',
    jsBuildPath = `${assetsBuildPath}js`,
    jsBuildFileName = 'main.js';

const
    jsLicensingInfo = '/* Licensing info */';

// Prepare Main CSS
const main_css = () => {
    return gulp.src([scssEntryFile])
        .pipe(concat(cssBuildFileName))
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(sass({outputStyle: 'compressed'})).on('error', sass.logError)
        .pipe(gulpif(!production, sourcemaps.write('.')))
        .pipe(gulp.dest(cssBuildPath));
};

// Prepare Main JS
const main_js = () => {
    return gulp.src(
        [`node_modules/govuk-frontend/govuk/all.js`],
        [`${assetsSrcPath}js/**`]
    )
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(babel({
            presets: [
                ['@babel/env', {
                    modules: false
                }]
            ]
        }))
        .pipe(uglify({
            // https://github.com/mishoo/UglifyJS#mangle-options
            mangle: {
                toplevel: false
            },
            // https://github.com/mishoo/UglifyJS#compress-options
            compress: {
                drop_console: production
            },
            // https://github.com/mishoo/UglifyJS#output-options
            output: {
                beautify: !production,
                preamble: jsLicensingInfo
            }
        }))
        .pipe(concat(jsBuildFileName))
        .pipe(gulpif(!production, sourcemaps.write('.')))
        .pipe(gulp.dest(jsBuildPath));
};

const copyFonts = () => {
    return gulp.src(`${govukAssets}fonts/*`)
        .pipe(gulp.dest(`${assetsBuildPath}/govuk-public/fonts`));
};

const copyImages = () => {
    return gulp.src(`${govukAssets}images/*`)
        .pipe(gulp.dest(`${assetsBuildPath}/govuk-public/images`));
};

// BrowserSync Init
const browserSyncInit = (browserSync) => {
    browserSync.init({
        notify: false,
        open: false,
        proxy: '127.0.0.1:9980',
        port: 9981,
        reloadDelay: 300,
        reloadDebounce: 500,
    });
};

// File watchers
const watchFiles = () => {
    const browserSync = require('browser-sync').create();
    browserSyncInit(browserSync);
    // gulp.watch('**/*.html').on('change', () => browserSync.reload());
    gulp.watch(`${assetsSrcPath}scss/**/*.scss`).on('change', () => {
        main_css(browserSync.stream());
        browserSync.reload();
    });
    gulp.watch(`${assetsSrcPath}js/**/*.js`).on('change', () => {
        main_js(browserSync.stream());
        browserSync.reload();
    });
};

const watchSCSS = () => {
    gulp.watch(`${assetsSrcPath}scss/**/*.scss`).on('change', () => {
        main_css();
    });
};

// Command definitions
const watch = watchFiles;
const watchscss = watchSCSS;
const css = main_css;
const js = main_js;
const build = gulp.parallel(css, js, copyFonts, copyImages);
const fe = gulp.series(build, watch);

// Export Commands
exports.css = css;
exports.js = js;
exports.watch = watch;
exports.watchscss = watchscss;
exports.build = build;
exports.fe = fe;

exports.default = fe;
