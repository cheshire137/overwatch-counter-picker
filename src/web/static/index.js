(function() {
  const fileInput = document.getElementById('file')
  const fileLabel = document.getElementById('file-input-label')
  const sampleScreenshot = document.getElementById('sample-screenshot-container')
  const previewContainer = document.getElementById('screenshot-preview-container')
  const preview = document.getElementById('screenshot-preview')
  const button = document.getElementById('submit-button')
  const allowedExtensions = ['jpg', 'jpeg', 'gif', 'png']
  const fileTypeWarning = document.getElementById('file-type-warning')

  function isFileTypeValid(fileName) {
    const fileNameParts = fileName.split('.')
    if (fileNameParts.length < 1) {
      return false
    }
    const extension = fileNameParts.pop().toLowerCase()
    return allowedExtensions.indexOf(extension) > -1
  }

  function fileSelected(file) {
    button.disabled = true

    fileLabel.setAttribute('data-original', fileLabel.textContent.trim())
    fileLabel.textContent = file.name

    if (!isFileTypeValid(file.name)) {
      fileTypeWarning.style.display = 'block'
      return
    }

    fileTypeWarning.style.display = 'none'
    button.disabled = false

    const reader = new FileReader()
    reader.addEventListener('load', function(event) {
      preview.src = event.target.result
      sampleScreenshot.style.display = 'none'
      previewContainer.style.display = 'block'
    })
    reader.readAsDataURL(file)
  }

  function noFileSelected() {
    button.disabled = true
    previewContainer.style.display = 'none'
    sampleScreenshot.style.display = 'block'
    fileLabel.textContent = fileLabel.getAttribute('data-original')
  }

  fileInput.addEventListener('change', function() {
    if (this.files && this.files[0]) {
      fileSelected(this.files[0])
    } else {
      noFileSelected()
    }
  })

  const form = document.getElementById('screenshot-upload-form')
  form.addEventListener('submit', function(event) {
    if (button.disabled) {
      event.preventDefault()
      return
    }

    button.disabled = true
    button.textContent = 'Uploading...'
  })

  button.disabled = true
})()
