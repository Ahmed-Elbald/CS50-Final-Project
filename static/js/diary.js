document.addEventListener('DOMContentLoaded', function () {
  let new_note_btn = document.querySelector('.new-diary-btn');
  let modal = new_note_btn.nextElementSibling;
  new_note_btn.addEventListener('click', function() {
    modal.showModal();
    let close_new_modal = modal.lastElementChild;
    close_new_modal.addEventListener('click', function() {
      modal.close();
    });
  });
  let open_btns = document.querySelectorAll('button.open-diary');
  let edit_btns = document.querySelectorAll('button.edit-diary');
  let delete_btns = document.querySelectorAll('button.delete-diary');
  for (let i = 0; i < open_btns.length; i++) {
    open_btns[i].addEventListener('click', function() {
      var diary = open_btns[i].previousElementSibling;
      diary.style.overflow = 'auto';
      diary.style.whiteSpace = 'break-spaces';
      var close_open = open_btns[i].nextElementSibling;
      while (close_open.className != 'close-diary') {
        close_open = close_open.nextElementSibling;
      };
      close_open.style.display = 'block';
      close_open.addEventListener('click', function() {
        diary.style.overflow = 'hidden';
        diary.style.whiteSpace = 'nowrap';
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
