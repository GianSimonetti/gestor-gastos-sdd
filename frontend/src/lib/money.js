const MONEY_PATTERN = /^[0-9]+\.[0-9]{2}$/;

export function parseMoneyInput(value) {
  if (!MONEY_PATTERN.test(value)) {
    return null;
  }
  const [units, cents] = value.split(".");
  return BigInt(units) * 100n + BigInt(cents);
}

export function formatMoneyInput(cents) {
  if (typeof cents !== "bigint") {
    throw new TypeError("Los centavos deben representarse con BigInt");
  }
  const sign = cents < 0n ? "-" : "";
  const absolute = cents < 0n ? -cents : cents;
  return `${sign}${absolute / 100n}.${String(absolute % 100n).padStart(2, "0")}`;
}
