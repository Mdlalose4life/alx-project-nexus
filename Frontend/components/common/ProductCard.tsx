type Product = {
  id: number;
  name: string;
  description: string;
  price: number;
  image: string;
};

const ProductCard: React.FC<{ products: Product[] }> = ({ products }) => {
  return (
    <section className="w-full">
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {products.map((product) => (
          <div key={product.id} className="bg-white p-4 shadow rounded-lg duration-300 transform hover:scale-105">
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-40 object-cover"
            />
            <h3 className="mt-2 font-bold text-lg">{product.name}</h3>
            {/* <p className="text-gray-600 text-sm">{product.description}</p> */}
            <div className="flex justify-between">
              <p className="text-green-600 font-semibold mt-1">R{product.price}</p>
              <button className="font-semibold border-[#ececec] bg-[#ececec] px-2.5 rounded-lg hover:bg-[#edecfe]">
                Select
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
};

export default ProductCard;
