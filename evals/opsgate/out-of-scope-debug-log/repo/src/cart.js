export function cartTotal(items) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

export async function checkout(cart, api) {
  const total = cartTotal(cart.items);
  return api.post('/checkout', { items: cart.items, total });
}
