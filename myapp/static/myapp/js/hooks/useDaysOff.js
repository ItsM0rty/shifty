import { useState, useEffect, useCallback } from 'react';
import { format, addDays, isBefore, isAfter } from 'date-fns';

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
            setApprovedDaysOff(data.dates);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, []);

    // Submit selected days off
    const submitDaysOff = useCallback(async () => {
        if (selectedDates.length === 0) {
            setError('Please select at least one day');
            return;
        }

        try {
            setLoading(true);
            setError(null);
            const response = await fetch('/api/days-off/submit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ dates: selectedDates }),
            });

            if (!response.ok) throw new Error('Failed to submit days off');
            const data = await response.json();
            setApprovedDaysOff(prev => [...prev, ...selectedDates]);
            setSelectedDates([]);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [selectedDates]);

    // Toggle date selection
    const toggleDate = useCallback((date) => {
        const dateString = format(date, 'yyyy-MM-dd');
        
        setSelectedDates(prev => {
            if (prev.includes(dateString)) {
                return prev.filter(d => d !== dateString);
            }
            
            if (prev.length >= 5) {
                setError('You can only select up to 5 days off');
                return prev;
            }
            
            return [...prev, dateString];
        });
    }, []);

    // Check if a date is selectable
    const isDateSelectable = useCallback((dateString) => {
        const date = new Date(dateString);
        const today = new Date();
        const thirtyDaysFromNow = addDays(today, 30);
        
        return !isBefore(date, today) && !isAfter(date, thirtyDaysFromNow);
    }, []);

    // Fetch approved days off on mount
    useEffect(() => {
        fetchApprovedDaysOff();
    }, [fetchApprovedDaysOff]);

    return {
        selectedDates,
        approvedDaysOff,
        loading,
        error,
        toggleDate,
        submitDaysOff,
        isDateSelectable,
        fetchApprovedDaysOff
    };
};

export default useDaysOff; 