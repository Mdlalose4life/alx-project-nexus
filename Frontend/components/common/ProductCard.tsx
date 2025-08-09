'use client'
import React, { useEffect, useState } from 'react';
import Link from "next/link";


type Product = {
  id: number;
  name: string;
  slug: string
  description: string;
  price: number;
  image: string;
};

const ProductCard: React.FC<{ products: Product[] }> = ({ products }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    const allproducts = async () => {
    const data = await fetch('/api/v1/products'); 
    if (!data.ok) {
      throw new Error('Network response was not ok');
    } 
    const result = await data.json();
    console.log("hello data", result);
    return result;
    setData()
  }
  allproducts();
  }, [])

  let index = 0; // Assuming you want to start from 0, adjust as needed
  return (
 
    <section className="w-full">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {products.map((product) => (
          <div key={product.id} className="bg-white p-3 h-[300px] shadow rounded-lg duration-300 transform hover:scale-105">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-[40%] lg:h-[70%] object-cover"
            />
            <h3 className="mt-2 font-semibold text-lg">{product.name}</h3>
            <p className="text-gray-600 text-sm">{product.description}</p>
            <div className="flex justify-between">
              <p className="text-green-600 font-semibold mt-1">R{product.price}</p>
              <Link
                href={`/product/${product.slug}`}
                className="font-semibold border-[#edecfe] bg-[#edecfe] px-2.5 rounded-lg hover:border-[#1c3454] hover:bg-[#c2c0f5]"
              >
                View
              </Link>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProductCard;
