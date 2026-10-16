export function formatArgentinaDate(isoDate) {
  if (!isoDate) return "";
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

export function formatMonth(monthValue) {
  if (!monthValue) return "";
  const [year, month] = monthValue.split("-");
  return `${month}/${year}`;
}
