import React, { useState } from 'react';
import { format } from 'date-fns';
import CalendarGrid from './CalendarGrid';
import useDaysOff from '../hooks/useDaysOff';
import './DaysOffCard.css';

const DaysOffCard = () => {
    const [currentDate, setCurrentDate] = useState(new Date());
    const {
        selectedDates,
        approvedDaysOff,
        loading,
        error,
        toggleDate,
        submitDaysOff,
        isDateSelectable
    } = useDaysOff();

    // Format date for display
    const formatDateForDisplay = (date) => {
        return format(new Date(date), 'MMM d');
    };

    // Navigate months
    const navigateMonth = (delta) => {
        setCurrentDate(prev => {
            const newDate = new Date(prev);
            newDate.setMonth(prev.getMonth() + delta);
            return newDate;
        });
    };

    return (
        <div className="days-off-card">
            {/* Header */}
            <div className="card-header">
                <h2 className="card-title">Select Days Off (5 max)</h2>
                <div className="selection-badge">
                    {selectedDates.length} / 5
                </div>
            </div>

            {/* Month Navigation */}
            <div className="month-navigation">
                <button
                    type="button"
                    onClick={() => navigateMonth(-1)}
                    className="nav-button"
                >
                    ←
                </button>
                <h3 className="month-title">
                    {format(currentDate, 'MMMM yyyy')}
                </h3>
                <button
                    type="button"
                    onClick={() => navigateMonth(1)}
                    className="nav-button"
                >
                    →
                </button>
            </div>

            {/* Calendar Grid */}
            <CalendarGrid
                currentDate={currentDate}
                selectedDates={selectedDates}
                approvedDaysOff={approvedDaysOff}
                onDateClick={toggleDate}
                isDateSelectable={isDateSelectable}
            />

            {/* Selected Dates */}
            <div className="selected-dates">
                {selectedDates.length > 0 ? (
                    <div className="date-pills">
                        {selectedDates.map(date => (
                            <div key={date} className="date-pill">
                                {formatDateForDisplay(date)}
                                <button
                                    className="remove-date"
                                    onClick={() => toggleDate(new Date(date))}
                                    type="button"
                                >
                                    ×
                                </button>
                            </div>
                        ))}
                    </div>
                ) : (
                    <div className="no-dates">No dates selected</div>
                )}
            </div>

            {/* Selection Info */}
            <div className="selection-info">
                You've selected {selectedDates.length} of 5 days
            </div>

            {/* Submit Button */}
            <button
                className="submit-button"
                onClick={submitDaysOff}
                disabled={loading || selectedDates.length === 0}
                type="button"
            >
                {loading ? (
                    <div className="button-spinner" />
                ) : (
                    'Submit Days Off'
                )}
            </button>

            {/* Error Message */}
            {error && (
                <div className="error-message">
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="20"
                        height="20"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    >
                        <circle cx="12" cy="12" r="10" />
                        <line x1="12" y1="8" x2="12" y2="12" />
                        <line x1="12" y1="16" x2="12.01" y2="16" />
                    </svg>
                    <span>{error}</span>
                </div>
            )}

            {/* Loading Overlay */}
            {loading && (
                <div className="loading-overlay">
                    <div className="spinner" />
                </div>
            )}
        </div>
    );
};

export default DaysOffCard; 