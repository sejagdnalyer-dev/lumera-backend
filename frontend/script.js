const API = "http://localhost:5000";

/* ======================
   MENU DATA
====================== */
const menuItems = [
    { id: 1, name: "Espresso", price: 120 },
    { id: 2, name: "Latte", price: 150 },
    { id: 3, name: "Cappuccino", price: 140 }
];


/* ======================
   LOAD MENU (menu.html)
====================== */
if (document.getElementById("menu")) {
    const menuDiv = document.getElementById("menu");

    menuItems.forEach(item => {
        menuDiv.innerHTML += `
            <div class="card">
                <h3>${item.name}</h3>
                <p>₱${item.price}</p>
                <button onclick="addToCart(${item.id})">Add</button>
            </div>
        `;
    });
}


/* ======================
   ADD TO CART
====================== */
function addToCart(id) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const item = menuItems.find(i => i.id === id);
    cart.push(item);

    localStorage.setItem("cart", JSON.stringify(cart));

    alert("Added to cart!");
}


/* ======================
   SHOW CART (cart.html)
====================== */
if (document.getElementById("cart")) {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let total = 0;

    const cartDiv = document.getElementById("cart");
    const totalDiv = document.getElementById("total");

    cartDiv.innerHTML = "";

    cart.forEach(item => {
        total += item.price;

        cartDiv.innerHTML += `
            <p>${item.name} - ₱${item.price}</p>
        `;
    });

    totalDiv.innerText = "Total: ₱" + total;
}


/* ======================
   GO TO CART
====================== */
function goCart() {
    window.location = "cart.html";
}


/* ======================
   CHECKOUT
====================== */
async function checkout() {
    let cart = JSON.parse(localStorage.getItem("cart")) || [];
    let user = JSON.parse(localStorage.getItem("user"));

    if (!cart.length) {
        alert("Cart is empty!");
        return;
    }

    if (!user) {
        alert("No user found!");
        return;
    }

    let total = cart.reduce((sum, item) => sum + item.price, 0);

    await fetch(API + "/order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            customer_id: user.id,
            items: cart,
            total: total
        })
    });

    alert("Order placed!");

    localStorage.removeItem("cart");
    window.location = "menu.html";
}