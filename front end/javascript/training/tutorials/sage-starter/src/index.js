// import React from "react";
// import ReactDOM from "react-dom";

// const element = <h1 title="web dev made simple">DevSage</h1>;

// const element = React.createElement(
//     "h1",
//     {
//         title: "Web Dev Made Simple"
//     },
//     "DevSage"
// )

// const root = document.getElementById("root")
// ReactDOM.render(element, root);

// Recreating the code above in pure JS
// const element = {
//     type: "h1",
//     props: {
//         title: "web dev made simple",
//         children: "DevSage"
//     }
// }


// // Get the root node
// const container = document.getElementById("root");

// // Create new element and add info from const element
// const node = document.createElement(element.type);
// node["title"] = element.props.title;

// // Add a new node and add in the metadata
// const text = document.createTextNode("");
// text["nodeValue"] = element.props.children

// // append back to container
// node.appendChild(text)
// container.appendChild(node)

// Create our own "render" and "create_element" functions

const Sage = {
    createElement,
    render
};

function createElement(type,props,...children){

    return {
        type,
        props: {
            ...props, // "..." is the spread operator
            children: children.map(child => {
                if(typeof child === "object") {
                    return child;
                } else {
                    return createTextElement(child);
                }
            })
        }
    }
};

function createTextElement(text){
    return {
        type: "TEXT_ELEMENT",
        props: {
            nodevalue: text,
            children: []
        }
    }
};

function render(element,container){
    // takes the element you want to insert, and the container you want to insert into

    // 1. Create DOM node

    const dom = element.type === "TEXT_ELEMENT" ? document.createTextNode("") : document.createElement(element.type);

    // 2. Add all properties/attributes
    Object.keys(element.props).filter(key => {
        if(key !== "children"){
            return true
        }
    })
    .forEach(propName =>{
        dom[propName] = element.props[propName]
    })

    // 3. Add all childre,
    element.props.children.forEach(child => render(child,dom));

    // 4. Render on screen

    container.appendChild(dom)

};


// This is called a "Pragma"
// It instructs "jsx" to use our custom functions defined above instead of React.createElement
/** @jsxRuntime classic */
/** @jsx Sage.createElement */
const element = <div style="background: orange; color:white">
    <h1 title="web dev made simple"> Sage Library </h1>
</div>;

const root = document.getElementById("root");
Sage.render(element,root)