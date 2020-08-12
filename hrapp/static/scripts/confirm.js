const deletePopup = document.getElementById("deleteText")
const message = document.getElementById("deleteMessage")
const closePopup = document.getElementById("closeDeleteText")
const deleteButton = document.getElementById("delete")

deleteButton.addEventListener("click", () => {
        message.innerText = "Are you sure you want to delete this computer?"
        deletePopup.show()
})

// Close the dialog when the close button is clicked
closePopup.addEventListener("click", e => deletePopup.close())

// Close the dialog when the escape key is pressed
window.addEventListener("keyup", e => {
    if (e.keyCode === 27) {
        deletePopup.close()
    }
})