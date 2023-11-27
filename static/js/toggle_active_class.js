function toggleActiveClass(element){
  const availableElements = element.parentNode.querySelectorAll("li");

  availableElements.forEach(function(availableElement) {
    availableElement.classList.remove("active");
  });

  element.classList.add("active")
}
