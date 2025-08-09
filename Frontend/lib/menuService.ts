export interface MenuItem {
  name: string;
  items: Record<string, string>;
}

export async function fetchCategories(): Promise<MenuItem> {
  const res = await fetch("/api/v1/product-categories");
  if (!res.ok) throw new Error("Failed to fetch categories");

  const data = await res.json();

  const items = data.results.reduce((acc: Record<string, string>, category: any, idx: number) => {
    acc[`item${idx + 1}`] = category.name;
    return acc;
  }, {});

  return {
    name: "Categories",
    items,
  };
}

export async function fetchBusinesses(): Promise<MenuItem> {
  const res = await fetch("/api/v1/businesses");
  if (!res.ok) throw new Error("Failed to fetch shops");

  const data = await res.json();

  const items = data.results.reduce(
    (acc: Record<string, string>, shop: any, idx: number) => {
      acc[`item${idx + 1}`] = shop.name;
      return acc;
    },
    {}
  );

  return {
    name: "Shops",
    items,
  };
}

export async function fetchLocations(): Promise<MenuItem> {
  const res = await fetch("/api/v1/businesses");
  if (!res.ok) throw new Error("Failed to fetch provinces");

  const data = await res.json();

  const provinces = data.results.filter((item: any) => item.type === "Province");

  const items = provinces.reduce(
    (acc: Record<string, string>, province: any, idx: number) => {
      acc[`item${idx + 1}`] = province.name;
      return acc;
    },
    {}
  );

  return {
    name: "Location",
    items,
  };
}



export async function fetchPrices(): Promise<MenuItem> {
    const res = await fetch("/api/v1/products");
    if (!res.ok) throw new Error("Failed to fetch products");

    const data = await res.json();

    const prices = data.results.map((product: any) => parseFloat(product.price));

    const priceRanges = [
        { label: "0 - 2k", min: 0, max: 2000 },
        { label: "2k - 4k", min: 2000, max: 4000 },
        { label: "4k - 6k", min: 4000, max: 6000 },
    ];

    const activeRanges = priceRanges.filter(range =>
        prices.some((price: number) => price >= range.min && price < range.max)
    );

    const items = activeRanges.reduce((acc: Record<string, string>, range, idx) => {
        acc[`item${idx + 1}`] = range.label;
        return acc;
    }, {});

    return {
        name: "Prices",
        items,
    };
}


export async function fetchAllMenus(): Promise<MenuItem[]> {
  const [categories, shops, locations, prices] = await Promise.all([
    fetchCategories(),
    fetchBusinesses(),
    fetchLocations(),
    fetchPrices(),
  ]);

  return [categories, shops, locations, prices];
}