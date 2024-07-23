const booksurl = "http://127.0.0.1:8000/";
const clothesurl= "http://localhost:8001/"

document.addEventListener("DOMContentLoaded", () => {
    fetchItems();

    document.getElementById("item-form").addEventListener("submit", (e) => {
        e.preventDefault();
        saveItem();
    });

    // document.getElementById("search-input").addEventListener("input", (e) => {
    //     searchItems(e.target.value);
    // });


});

async function fetchItems() {
    const booksResponse = await fetch(`http://localhost:8000/books/`);
    const books = await booksResponse.json();

    const clothesResponse = await fetch(`http://localhost:8001/clothes/`);
    const clothes = await clothesResponse.json();

    displayItems(books, "book");
     displayItemsclothes(clothes, "clothes");
    //console.log(clothes);
}

function displayItems(items, type) {
    const container = document.getElementById("card-container");
   // Clear the container

    items.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        var rate = Math.round(item.rating * 100) / 100;
       
        var name = type === "book" ? item.name : item.material;
        // console.log(name);
        card.innerHTML = `
         <img src="book.jpeg" alt="Description of image">
            <h3>${type === "book" ? item.name : item.material}</h3>
            <p>${type === "book" ? "Author: " + item.author : "Size: " + item.type}</p>
           
            <p>Rating: ${rate}</p>
           <button onclick="addtowishlist(${item.id}, '${type}', '${item.name.replace(/'/g, "\\'").replace(/"/g, '\\"')}')"> &#9829;</button>


           
            <button class = "give-rating" onclick="editItem(${item.id}, '${type}')">Give Rating</button> 
      
            
        `;
        container.appendChild(card);
    });
}
{/* <button onclick="deleteItem(${item.id}, '${type}')">Delete</button> */}
function displayItemsclothes(items, type) {
    const container = document.getElementById("card-containertwo");
     // Clear the container

   
    items.forEach(item => {
        const card = document.createElement("div");
        card.className = "card";
        var name = type === "book" ? item.name : item.material;
        var rate = Math.round(item.rating * 100) / 100;
      //  console.log(item);
        card.innerHTML = `
         <img src="image.png" alt="Description of image">
            <h3>${type === "book" ? item.name : item.material}</h3>
            <p>${type === "book" ? "Author: " + item.author : "Type: " + item.type}</p>
            
            
            <p>Rating: ${rate}</p>
      
          
             <button onclick="addtowishlist(${item.id}, '${type}','${name}')"> &#9829;</button>
              <button  class = "nored" onclick="editItem(${item.id}, '${type}')">Give Rating</button> 
        `;
        container.appendChild(card);
    });
}

async function addtowishlist(itemId, type, itemName) {
    // console.log("abc");
    const email =  localStorage.getItem('email');
    // localStorage.getItem('email');
    if (!email) {
        alert('Please log in to add items to your wishlist.');
        return;
    }

    fetch(`http://127.0.0.1:9009/users/${email}/wishlist/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({  item_id: itemId , item_name : itemName}),
    })
    .then(response => response.json())
    .then(data => {
        // console.log(data);
        // console.log("success");
        //alert('Item added to wishlist');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

async function saveItem() {
    const id = document.getElementById("item-id").value;
    const type = document.getElementById("item-type").value;
    const title = document.getElementById("item-title").value;
    const author = document.getElementById("item-author").value;
    const description = document.getElementById("item-description").value;

    let item;

    if (type === "book") {
        item = {
            name: title,
            author: author,
            rating: description
        };
    } else {
        item = {
            material: title,
            type: author,
            rating: description
        };
    }
    const url = type=="book"?`${booksurl}books/`:`${clothesurl}clothes/`;
    const url2 = id ? type=="book"?`${booksurl}books/${id}`:`${clothesurl}clothes/${id}` : url;
    const method = id ? "PUT" : "POST";

// console.log(item);
// console.log(url);
    const response = await fetch(url2, {
        method ,
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(item)
    });

    if (response.ok) {
        const container = document.getElementById("card-container");
        container.innerHTML = "";
        fetchItems();
        document.getElementById("item-form").reset();
    }
}

async function editItem(id, type) {
    var formContainer = document.querySelector('.form-container');
  
        formContainer.scrollIntoView({ behavior: 'smooth' });
  
    const response = type ==="book"? await fetch(`${booksurl}books/${id}`):await fetch(`${clothesurl}clothes/${id}`);
    const item = await response.json();
    // console.log(item);

   document.getElementById("item-id").value = item.id;
    document.getElementById("item-type").value = type;
    document.getElementById("item-title").value = type === "book" ? item.name: item.material;
    document.getElementById("item-author").value = type === "book" ? item.author : item.type;
    document.getElementById("item-description").value = "";
}

async function deleteItem(id, type) {
    const deteurl = type=="books"?booksurl:clothesurl;
    const response = await fetch(`${deteurl}books/${id}`, {
        method: "DELETE"
    });

    if (response.ok) {
        const container = document.getElementById("card-container");
        container.innerHTML = "";
        fetchItems();
    }
   
} 

async function searchItems(query) {

    var searchValue = document.getElementById('search-input').value;
    if(searchValue ==="")  fetchItems();
    else{
   const url = "http://127.0.0.1:9001/";
    const booksResponse = await fetch(`${url}search/${searchValue}`);
    if (!booksResponse.ok) {
        document.getElementById('search-input').value = '';
    }

  else{  const item = await booksResponse.json();
    console.log(item);
const type = item.kind;
const container = document.getElementById("card-container");
container.innerHTML = "";
const container2 = document.getElementById("card-containertwo");
container2.innerHTML = "";
const card = document.createElement("div");
card.className = "card";
card.innerHTML = `
     <img src="${ type ==="books"? "book.jpeg" : "image.png"}" alt="Description of image">
    <h3>${type === "books" ? item.name : item.material}</h3>
    <p>${type === "books" ? "Author: " + item.author : "Type " + item.type}</p>
    <p>Description: ${item.rating}</p>

    <button onclick="deleteItem(${item.id}, '${type}')">Delete</button>
`;
if(type=="books")
container.appendChild(card);
else
container2.appendChild(card);
  }
}
}
