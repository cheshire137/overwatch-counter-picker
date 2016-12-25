(function() {
  const input = document.getElementById('file')
  const sampleScreenshot = document.getElementById('sample-screenshot-container')
  const previewContainer = document.getElementById('screenshot-preview-container')
  const preview = document.getElementById('screenshot-preview')

  input.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      const reader = new FileReader()
      reader.addEventListener('load', function(event) {
        preview.src = event.target.result
        sampleScreenshot.style.display = 'none'
        previewContainer.style.display = 'block'
      })
      reader.readAsDataURL(this.files[0])
    } else {
      previewContainer.style.display = 'none'
      sampleScreenshot.style.display = 'block'
    }
  })
})()
