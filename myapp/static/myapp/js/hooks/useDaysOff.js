import { useState, useEffect, useCallback } from 'react';
import { format, isPast, addDays, isAfter } from 'date-fns';

const MAX_SELECTIONS = 5;
const MAX_DAYS_AHEAD = 30;

const useDaysOff = () => {
    const [selectedDates, setSelectedDates] = useState([]);
    const [approvedDaysOff, setApprovedDaysOff] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch approved days off
    const fetchApprovedDaysOff = useCallback(async () => {
        try {
            setLoading(true);
            setError(null);
            
            const response = await fetch('/api/days-off/approved/');
            if (!response.ok) throw new Error('Failed to fetch approved days off');
            
            const data = await response.json();
            setApprovedDaysOff(data);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    // Load approved days off on mount
    useEffect(() => {
        fetchApprovedDaysOff();
    }, [fetchApprovedDaysOff]);

    // Toggle date selection
    const toggleDate = useCallback((dateString) => {
        setSelectedDates(prev => {
            const index = prev.indexOf(dateString);
            
            if (index === -1) {
                if (prev.length >= MAX_SELECTIONS) {
                    setError(`You can only select up to ${MAX_SELECTIONS} days off`);
                    return prev;
                }
                return [...prev, dateString];
            }
            
            return prev.filter(date => date !== dateString);
        });
    }, []);

    // Submit days off
    const submitDaysOff = useCallback(async () => {
        if (selectedDates.length === 0) {
            setError('Please select at least one day off');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            
            const response = await fetch('/api/days-off/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ dates: selectedDates })
            });
            
            if (!response.ok) throw new Error('Failed to submit days off');
            
            // Update approved days off
            setApprovedDaysOff(prev => [...prev, ...selectedDates]);
            setSelectedDates([]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [selectedDates]);

    // Check if date is selectable
    const isDateSelectable = useCallback((date) => {
        const dateObj = new Date(date);
        const maxDate = addDays(new Date(), MAX_DAYS_AHEAD);
        
        return !isPast(dateObj) && !isAfter(dateObj, maxDate);
    }, []);

    return {
        selectedDates,
        approvedDaysOff,
        loading,
        error,
        toggleDate,
        submitDaysOff,
        isDateSelectable
    };
};

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default useDaysOff; 