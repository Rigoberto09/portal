const btneliminar = Document.querySekectirAll('.eliminarC')
if (btneliminar){
    const btarray =Array.from(btneliminar);
    btarray.forEach((btn)=>{
        btn.addEventListener('click',(e) =>{
            if(!confirm('Estas seguro de eliminar?')){
                e.priventDefault();
            }
        })
    })
}