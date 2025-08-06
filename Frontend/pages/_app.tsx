import Layout from "@/components/layouts/Layout";
import { MenuProvider } from "@/store/MenuContext";
import "@/styles/globals.css";
import type { AppProps } from "next/app";

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MenuProvider> 
      <Layout>
        <Component {...pageProps} />
      </Layout>
    </MenuProvider>
  );
}
