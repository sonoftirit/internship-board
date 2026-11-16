import { expect, test } from 'vitest'
import { timeAgo } from './timeAgo.js'

const NOW = new Date('2026-11-16T12:00:00Z')
const ONE_DAY_MS = 24 * 60 * 60 * 1000

function daysBefore(days) {
  return new Date(NOW.getTime() - days * ONE_DAY_MS).toISOString()
}

test('less than a full day ago is "today"', () => {
  expect(timeAgo(daysBefore(0), NOW)).toBe('today')
  expect(timeAgo(daysBefore(0.9), NOW)).toBe('today')
})

test('exactly one day uses the singular "day"', () => {
  expect(timeAgo(daysBefore(1), NOW)).toBe('1 day ago')
})

test('several days', () => {
  expect(timeAgo(daysBefore(5), NOW)).toBe('5 days ago')
  expect(timeAgo(daysBefore(29), NOW)).toBe('29 days ago')
})

test('30 days or more is shown in months', () => {
  expect(timeAgo(daysBefore(30), NOW)).toBe('1 month ago')
  expect(timeAgo(daysBefore(65), NOW)).toBe('2 months ago')
})

test('a date slightly in the future (clocks differ) is "today"', () => {
  expect(timeAgo(daysBefore(-1), NOW)).toBe('today')
})
