let fields = document.getElementsByTagName('textarea');
fields.array.forEach(element => {
    element.value.split(' ').join('');
});