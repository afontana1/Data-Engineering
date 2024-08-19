// by defualt every stream is in Flow mode
process.stdin.on("data", input => {
  let userTxt = input.toString().trim();
  console.log("user: ", userTxt);
});
// DETAILS:
//non flow meaning we need to ask for the new data