import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import App from './App';
import { describe, it, expect } from 'vitest';

describe('App', () => {
    it('renders standard navigation', () => {
        render(
            <MemoryRouter>
                <App />
            </MemoryRouter>
        );
        expect(screen.getAllByText(/Intellify/i).length).toBeGreaterThan(0);
    });
});
