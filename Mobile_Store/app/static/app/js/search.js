// seach theo text or theo image
function toggleUploadButton() {
    const searchInput = document.getElementById("search-input");
    const imageUpload = document.getElementById("image-upload");
  
    // Enable or disable the image upload input based on the search input
    imageUpload.disabled = searchInput.value.length > 0;
  }
  
  function toggleSearchInput() {
    const searchInput = document.getElementById("search-input");
    const imageUpload = document.getElementById("image-upload");
  
    // Enable or disable the search input based on the image upload
    searchInput.disabled = imageUpload.files.length > 0;
  }
  
  function handleSearch(event) {
    const searchInput = document.getElementById("search-input").value;
    const imageUpload = document.getElementById("image-upload").files.length;
  
    // Change the action based on the inputs
    if (searchInput) {
      event.currentTarget.action = "{% url 'search' %}"; // Text search
    } else if (imageUpload) {
      event.currentTarget.action = "{% url 'image_search' %}"; // Image search
    } else {
      event.preventDefault(); // Prevent form submission if no input
      alert("Please enter a search term or upload an image.");
    }
  }
  