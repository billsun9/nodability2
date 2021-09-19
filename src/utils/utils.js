const contentLongEnough = (s, len) => {
    if(s.split(" ").length < len) {
      return false;
    }
    return true
}

export {contentLongEnough}