export default name => {
  if (document.getElementsByName(name).length > 0) {
    return document.getElementsByName(name)[0].content;
  } else {
    return null;
  }
};
