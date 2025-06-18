import React from 'react';
import PropTypes from 'prop-types';
import { startOfMonth, endOfMonth, eachDayOfInterval, startOfWeek, endOfWeek } from 'date-fns';
import CalendarCell from './CalendarCell';

const WEEKDAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

const CalendarGrid = ({ currentDate, selectedDates, approvedDaysOff, onDateClick, isDateSelectable }) => {
    const generateWeeks = () => {
        const monthStart = startOfMonth(currentDate);
        const monthEnd = endOfMonth(currentDate);
        const calendarStart = startOfWeek(monthStart);
        const calendarEnd = endOfWeek(monthEnd);

        const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });
        const weeks = [];
        let currentWeek = [];

        days.forEach((date, index) => {
            currentWeek.push(date);
            if ((index + 1) % 7 === 0) {
                weeks.push(currentWeek);
                currentWeek = [];
            }
        });

        return weeks;
    };

    return (
        <table className="calendar-grid">
            <thead>
                <tr>
                    {WEEKDAYS.map(day => (
                        <th key={day} className="weekday">
                            {day}
                        </th>
                    ))}
                </tr>
            </thead>
            <tbody>
                {generateWeeks().map((week, weekIndex) => (
                    <tr key={weekIndex}>
                        {week.map(date => {
                            const dateString = date.toISOString().split('T')[0];
                            const isSelected = selectedDates.includes(dateString);
                            const isSubmitted = approvedDaysOff.includes(dateString);
                            const isDisabled = !isDateSelectable(dateString);
                            const isPast = date < new Date();

                            return (
                                <CalendarCell
                                    key={dateString}
                                    date={date}
                                    isSelected={isSelected}
                                    isDisabled={isDisabled}
                                    isPast={isPast}
                                    isSubmitted={isSubmitted}
                                    onClick={onDateClick}
                                />
                            );
                        })}
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

CalendarGrid.propTypes = {
    currentDate: PropTypes.instanceOf(Date).isRequired,
    selectedDates: PropTypes.arrayOf(PropTypes.string).isRequired,
    approvedDaysOff: PropTypes.arrayOf(PropTypes.string).isRequired,
    onDateClick: PropTypes.func.isRequired,
    isDateSelectable: PropTypes.func.isRequired
};

export default CalendarGrid; 