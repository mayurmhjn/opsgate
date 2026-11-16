const API_URL = import.meta.env.VITE_API_URL;

export async function getOrders() {
  const res = await fetch(`${API_URL}/orders`);
  return res.json();
}
