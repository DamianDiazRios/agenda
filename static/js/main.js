const btnDelete = document.querySelectorAll('.btn-delete')

if(btnDelete) {
    const btnArray = Array.from(btnDelete);
    btnArray.forEach((btn)) => {
        btn.addEventsListener('click', (e) => {
         if(!confirm('Estas seguro que quieres borrarlo?')) {
            e.preventDefault();
         }
       });
     });
    }