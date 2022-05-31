import { initAll } from "govuk-frontend/govuk/all";
var CookiePolicy = require("./modules/cookie-policy");
initAll();

var cookiePolicy = new CookiePolicy();
cookiePolicy.initBanner(".app-cookie-banner", ".js-accept-cookie", "cookies");
