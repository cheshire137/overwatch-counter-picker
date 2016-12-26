(function() {
  const input = document.getElementById('file')
  const sampleScreenshot = document.getElementById('sample-screenshot-container')
  const previewContainer = document.getElementById('screenshot-preview-container')
  const preview = document.getElementById('screenshot-preview')
  const button = document.getElementById('submit-button')

  input.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      button.disabled = false
      const reader = new FileReader()
      reader.addEventListener('load', function(event) {
        preview.src = event.target.result
        sampleScreenshot.style.display = 'none'
        previewContainer.style.display = 'block'
      })
      reader.readAsDataURL(this.files[0])
    } else {
      button.disabled = true
      previewContainer.style.display = 'none'
      sampleScreenshot.style.display = 'block'
    }
  })

  const form = document.getElementById('screenshot-upload-form')
  form.addEventListener('submit', function(event) {
    button.disabled = true
    button.textContent = 'Uploading...'
  })

  button.disabled = true
})()
