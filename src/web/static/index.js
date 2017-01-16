(function() {
  const fileInput = document.getElementById('file')
  const fileLabel = document.getElementById('file-input-label')
  const sampleScreenshot = document.getElementById('sample-screenshot-container')
  const previewContainer = document.getElementById('screenshot-preview-container')
  const preview = document.getElementById('screenshot-preview')
  const button = document.getElementById('submit-button')
  const allowedExtensions = ['jpg', 'jpeg', 'gif', 'png']
  const fileTypeWarning = document.getElementById('file-type-warning')
  const form = document.getElementById('screenshot-upload-form')
  const nextScrButton = document.getElementById('next-screenshot-button')
  const prevScrButton = document.getElementById('prev-screenshot-button')
  const scrList = document.getElementById('sample-screenshots')

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

  form.addEventListener('submit', function(event) {
    if (button.disabled) {
      event.preventDefault()
      return
    }

    button.disabled = true
    button.textContent = 'Uploading...'
  })

  button.disabled = true

  function dragHandler(event) {
    if (event.dataTransfer.types.indexOf('Files') < 0) {
      return
    }
    event.preventDefault()
    event.stopPropagation()
    const srcElement = event.srcElement ? event.srcElement : event.target
    const isTarget = srcElement.id === 'file-input-label'
    event.dataTransfer.dropEffect = isTarget ? 'copy' : 'none'
    if (event.type === 'dragover') {
      fileLabel.classList.add('focus')
    } else if (event.type === 'drop') {
      fileInput.files = event.dataTransfer.files
      if (!button.disabled) {
        button.disabled = true
        form.submit()
      }
    }
    if (!isTarget) {
      fileLabel.classList.remove('focus')
    }
  }

  document.body.addEventListener('dragleave', dragHandler)
  document.body.addEventListener('dragover', dragHandler)
  document.body.addEventListener('drop', dragHandler)

  function changeActiveScreenshot(nextModifier) {
    const active = scrList.querySelector('.active.screenshot')
    active.classList.remove('active')
    active.style.display = 'none'
    const screenshots = Array.from(scrList.querySelectorAll('.screenshot'))
    const numScreenshots = screenshots.length
    const index = screenshots.indexOf(active)
    const nextIndex = (index + nextModifier) % numScreenshots
    const newActive = screenshots[nextIndex]
    newActive.classList.add('active')
    newActive.style.display = 'inline'
    if (nextIndex === 0) {
      prevScrButton.style.display = 'none'
      nextScrButton.style.display = 'inline-flex'
    } else if (nextIndex === numScreenshots - 1) {
      prevScrButton.style.display = 'inline-flex'
      nextScrButton.style.display = 'none'
    } else {
      prevScrButton.style.display = 'inline-flex'
      nextScrButton.style.display = 'inline-flex'
    }
  }

  nextScrButton.addEventListener('click', function() {
    changeActiveScreenshot(1)
  })
  prevScrButton.addEventListener('click', function() {
    changeActiveScreenshot(-1)
  })
})()
