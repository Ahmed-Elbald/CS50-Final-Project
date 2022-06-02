document.addEventListener('DOMContentLoaded', function () {
  let new_note_btn = document.querySelector('.new-note-btn');
  let modal = new_note_btn.nextElementSibling;
  new_note_btn.addEventListener('click', function() {
    modal.showModal();
    let close_new_modal = modal.lastElementChild;
    close_new_modal.addEventListener('click', function() {
      modal.close();
    });
  });
  let open_btns = document.querySelectorAll('button.open-note');
  let edit_btns = document.querySelectorAll('button.edit-note');
  let delete_btns = document.querySelectorAll('button.delete-note');
  for (let i = 0; i < open_btns.length; i++) {
    open_btns[i].addEventListener('click', function() {
      var note = open_btns[i].previousElementSibling;
      note.style.overflow = 'auto';
      note.style.whiteSpace = 'inherit';
      var close_open = open_btns[i].nextElementSibling;
      while (close_open.className != 'close-note') {
        close_open = close_open.nextElementSibling;
      };
      close_open.style.display = 'block';
      close_open.addEventListener('click', function() {
        note.style.overflow = 'hidden';
        note.style.whiteSpace = 'nowrap';
        close_open.style.display = 'none';
      });
    });
    edit_btns[i].addEventListener('click', function() {
      let modal = edit_btns[i].nextElementSibling;
      while (modal.className.includes('edit-modal') == false) {
        modal = modal.nextElementSibling;
      };
      modal.showModal();
      let close_edit = modal.lastElementChild;
      close_edit.addEventListener('click', function() {
        modal.close();
      });
    });
    delete_btns[i].addEventListener('click', function() {
      let modal = edit_btns[i].nextElementSibling;
      while (modal.className.includes('delete-modal') == false) {
        modal = modal.nextElementSibling;
      };
      modal.showModal();
      let close_edit = modal.lastElementChild;
      close_edit.addEventListener('click', function() {
        modal.close();
      });
    });
  };
});
