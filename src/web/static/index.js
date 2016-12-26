(function() {
  const fileInput = document.getElementById('file')
  const fileLabel = document.getElementById('file-input-label')
  const sampleScreenshot = document.getElementById('sample-screenshot-container')
  const previewContainer = document.getElementById('screenshot-preview-container')
  const preview = document.getElementById('screenshot-preview')
  const button = document.getElementById('submit-button')

  function fileSelected(file, event) {
    button.disabled = false

    const reader = new FileReader()
    reader.addEventListener('load', function(event) {
      preview.src = event.target.result
      sampleScreenshot.style.display = 'none'
      previewContainer.style.display = 'block'
    })
    reader.readAsDataURL(file)

    fileLabel.setAttribute('data-original', fileLabel.textContent.trim())
    fileLabel.textContent = event.target.value.split('\\').pop()
  }

  function noFileSelected() {
    button.disabled = true
    previewContainer.style.display = 'none'
    sampleScreenshot.style.display = 'block'
    fileLabel.textContent = fileLabel.getAttribute('data-original')
  }

  fileInput.addEventListener('change', function(event) {
    if (this.files && this.files[0]) {
      fileSelected(this.files[0], event)
    } else {
      noFileSelected()
    }
  })

  const form = document.getElementById('screenshot-upload-form')
  form.addEventListener('submit', function(event) {
    button.disabled = true
    button.textContent = 'Uploading...'
  })

  button.disabled = true
})()
