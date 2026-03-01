import '@testing-library/jest-dom';
import { vi } from 'vitest';

class IntersectionObserverMock {
    observe = vi.fn();
    disconnect = vi.fn();
    takeRecords = vi.fn();
    unobserve = vi.fn();
}

vi.stubGlobal('IntersectionObserver', IntersectionObserverMock);
