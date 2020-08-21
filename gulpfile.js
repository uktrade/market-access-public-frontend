'use strict';

const
    gulp = require('gulp'),
    concat = require('gulp-concat'),
    gulpif = require('gulp-if'),
    sass = require('gulp-sass'),
    babel = require('gulp-babel'),
    browserSync = require('browser-sync').create(),
    sourcemaps = require('gulp-sourcemaps'),
    uglify = require('gulp-uglify');


// NOTES
// Useful tips for uglifying - https://stackoverflow.com/questions/24591854/using-gulp-to-concatenate-and-uglify-files


const production = ((process.env.NODE_ENV || 'dev').trim().toLowerCase() === 'production');

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

// BrowserSync Init
const browserSyncInit = () => {
    browserSync.init({
        notify: false,
        open: false,
        proxy: '127.0.0.1:9980',
        port: 9981,
        reloadDelay: 300,
        reloadDebounce: 500,
    });
};

// Prepare Main CSS
const main_css = () => {
    return gulp.src([scssEntryFile])
        .pipe(concat(cssBuildFileName))
        .pipe(gulpif(!production, sourcemaps.init()))
        .pipe(sass({outputStyle: 'compressed'})).on('error', sass.logError)
        .pipe(gulpif(!production, sourcemaps.write('.')))
        .pipe(gulp.dest(cssBuildPath))
        .pipe(browserSync.stream());
};

// Prepare Main JS
const main_js = () => {
    return gulp.src([
        `${assetsSrcPath}js/**`,
    ])
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
        .pipe(gulp.dest(jsBuildPath))
        .pipe(browserSync.stream());
};

const copyFonts = () => {
    return gulp.src(`${govukAssets}fonts/*`)
        .pipe(gulp.dest(`${assetsBuildPath}/govuk-public/fonts`));
};

const copyImages = () => {
    return gulp.src(`${govukAssets}images/*`)
        .pipe(gulp.dest(`${assetsBuildPath}/govuk-public/images`));
};

// File watchers
const watchFiles = () => {
    browserSyncInit();
    // gulp.watch('**/*.html').on('change', () => browserSync.reload());
    gulp.watch(`${assetsSrcPath}scss/**/*.scss`).on('change', () => {
        main_css();
        browserSync.reload();
    });
    gulp.watch(`${assetsSrcPath}js/**/*.js`).on('change', () => {
        main_js();
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
