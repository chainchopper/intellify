import { render, screen } from '@testing-library/react';
import App from './App';
import { describe, it, expect } from 'vitest';

describe('App Dashboard', () => {
    it('renders the sidebar and topbar correctly', () => {
        render(<App />);
        expect(screen.getAllByText(/Intellify/i).length).toBeGreaterThan(0);
    });
});
