// Опциональная цепочка и nullish coalescing
const name = user?.profile?.name ?? 'Гость';

// Array methods
const active = users
  .filter(u => u.active)
  .map(u => u.name)
  .sort();

// Object.entries
Object.entries(config).forEach(([key, value]) => {
  console.log(key, value);
});

const storage = {
  get(key, fallback = null) {
    try {
      return JSON.parse(localStorage.getItem(key)) ?? fallback;
    } catch {
      return fallback;
    }
  },
  set(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
  }
};

storage.set('theme', 'dark');
console.log(storage.get('theme')); // 'dark'

