export default function Cart({ items }) {
  const total = items.reduce(
    (sum, item) => sum + item.price * item.quantity * (1 - item.discount),
    0
  );
  return <p>Total: {total.toFixed(2)}</p>;
}
