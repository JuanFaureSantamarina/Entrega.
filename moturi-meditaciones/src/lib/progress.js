"use client";

/**
 * Progreso local del Desafío de 10 días.
 * Se guarda únicamente en el dispositivo del usuario (localStorage).
 * No hay cuentas ni backend: si cambia de dispositivo, el progreso no viaja.
 */

const STORAGE_KEY = "moturi:desafio-10-dias:progreso";
const TOTAL_DAYS = 10;

function safeGetStorage() {
  if (typeof window === "undefined") return null;
  try {
    return window.localStorage;
  } catch {
    // localStorage puede no estar disponible (modo privado, permisos, etc.)
    return null;
  }
}

export function getCompletedDays() {
  const storage = safeGetStorage();
  if (!storage) return [];
  try {
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    if (!Array.isArray(parsed)) return [];
    return parsed.filter((day) => Number.isInteger(day) && day >= 1 && day <= TOTAL_DAYS);
  } catch {
    return [];
  }
}

export function isDayCompleted(day) {
  return getCompletedDays().includes(Number(day));
}

export function setDayCompleted(day, completed) {
  const storage = safeGetStorage();
  if (!storage) return getCompletedDays();

  const current = new Set(getCompletedDays());
  if (completed) {
    current.add(Number(day));
  } else {
    current.delete(Number(day));
  }

  const next = Array.from(current).sort((a, b) => a - b);
  try {
    storage.setItem(STORAGE_KEY, JSON.stringify(next));
  } catch {
    // Si falla el guardado, seguimos devolviendo el estado en memoria.
  }
  return next;
}

export function toggleDayCompleted(day) {
  return setDayCompleted(day, !isDayCompleted(day));
}

export function getProgressCount() {
  return getCompletedDays().length;
}

export const CHALLENGE_TOTAL_DAYS = TOTAL_DAYS;
