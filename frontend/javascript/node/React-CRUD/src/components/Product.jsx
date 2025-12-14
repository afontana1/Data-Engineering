import axios from "axios";
import { Link } from "react-router-dom";
import { toast } from "react-toastify";
import Swal from "sweetalert2";
import { VITE_BACKEND_URL } from "../App";

/* eslint-disable react/prop-types */
const Product = ({ product, getProducts }) => {

    const deleteProduct = async (id) => {
        const result = await Swal.fire({
            title: 'Do you really want to delete the product?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, delete it!'

        })
        if(result.isConfirmed){
            try{
                await axios.delete(`${VITE_BACKEND_URL}/api/products/${id}`);
                toast.success("Delete a product successfully");
                getProducts();
            }catch(error){
                toast.error(error.message);
            }
        }

    }

    return (
        <div className="bg-white rounded shadow-lg overflow-hidden">
            <img src={product.image} className="w-full h-28 object-cover" />
            <div className="px-4 pt-2 pb-4">
                <h2 className="text font-semibold">{product.name}</h2>
                <div className="text-sm">Quantity: {product.quantity}</div>
                <div className="text-sm">Price ${product.price}</div>

                <div className="mt-2 flex gap-4">
                    <Link to={`/edit/${product._id}`} className="inline-block w-full text-center shadow-md text-sm bg-gray-700 text-white rounded-sm px-4 py-1 font-bold hover:bg-gray-600 hover:cursor-pointer">Edit</Link>
                    <button onClick={() => deleteProduct(product._id)}  className="inline-block w-full text-center shadow-md text-sm bg-red-700 text-white rounded-sm px-4 py-1 font-bold hover:bg-red-600 hover:cursor-pointer">Delete</button>
                </div>


            </div>
         

        </div>
    )
}

export default Product;
