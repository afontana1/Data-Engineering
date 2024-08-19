// Implement the Gatsby API “onCreatePage”. This is
// called after every page is created.
exports.onCreatePage = async ({ page, actions }) => {
  const { createPage } = actions;

  // page.matchPath is a special key that's used for matching pages
  // only on the client.
  console.log(page.path);
  if (page.path.match(/^\/app/)) {
    console.log("Is Match!");
    page.matchPath = "/app/*";

    // Update the page.
    createPage(page);
  }
};
