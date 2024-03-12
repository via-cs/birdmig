const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    createProxyMiddleware("/profile", {
      target: "http://backend:5000",
      changeOrigin: true,
    })
  );
};
