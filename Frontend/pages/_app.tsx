import Layout from "@/components/layouts/Layout";
import { CartProvider } from "@/store/CartContext";
import { MenuProvider } from "@/store/menuContext";
import "@/styles/globals.css";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MenuProvider> 
      <Layout>
        <CartProvider>
          <Component {...pageProps} />
        </CartProvider>
      </Layout>
    </MenuProvider>
  );
}
