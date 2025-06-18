import React, { useState } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameMonth, isToday } from 'date-fns';
import CalendarCell from './CalendarCell';
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

    // Generate calendar days
    const generateCalendarDays = () => {
        const monthStart = startOfMonth(currentDate);
        const monthEnd = endOfMonth(currentDate);
        const days = eachDayOfInterval({ start: monthStart, end: monthEnd });
        
        // Add empty cells for days before month start
        const startDay = monthStart.getDay();
        const emptyStartCells = Array(startDay).fill(null);
        
        return [...emptyStartCells, ...days];
    };

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

            {/* Calendar Grid */}
            <div className="calendar-grid">
                {/* Weekday headers */}
                <div className="weekday">Sun</div>
                <div className="weekday">Mon</div>
                <div className="weekday">Tue</div>
                <div className="weekday">Wed</div>
                <div className="weekday">Thu</div>
                <div className="weekday">Fri</div>
                <div className="weekday">Sat</div>

                {/* Calendar days */}
                {generateCalendarDays().map((date, index) => {
                    if (!date) {
                        return <div key={`empty-${index}`} className="calendar-cell empty" />;
                    }

                    const dateString = format(date, 'yyyy-MM-dd');
                    const isSelected = selectedDates.includes(dateString);
                    const isSubmitted = approvedDaysOff.includes(dateString);
                    const isDisabled = !isDateSelectable(dateString);
                    const isPast = isPast(date);

                    return (
                        <CalendarCell
                            key={dateString}
                            day={date.getDate()}
                            date={dateString}
                            isSelected={isSelected}
                            isDisabled={isDisabled}
                            isPast={isPast}
                            isSubmitted={isSubmitted}
                            onClick={toggleDate}
                        />
                    );
                })}
            </div>

            {/* Selected Dates */}
            <div className="selected-dates">
                {selectedDates.length > 0 ? (
                    <div className="date-pills">
                        {selectedDates.map(date => (
                            <div key={date} className="date-pill">
                                {formatDateForDisplay(date)}
                                <button
                                    className="remove-date"
                                    onClick={() => toggleDate(date)}
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