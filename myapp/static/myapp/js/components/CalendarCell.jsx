import React from 'react';
import PropTypes from 'prop-types';

const CalendarCell = ({ date, isDisabled, isSelected, isPast, isSubmitted, onClick }) => {
    if (!date) {
        return <td className="calendar-cell empty" />;
    }

    const handleClick = () => {
        if (!isDisabled) {
            onClick(date);
        }
    };

    const getCellClasses = () => {
        const classes = ['calendar-cell'];
        if (isSelected) classes.push('selected');
        if (isDisabled) classes.push('disabled');
        if (isPast) classes.push('past');
        if (isSubmitted) classes.push('submitted');
        return classes.join(' ');
    };

    return (
        <td className={getCellClasses()}>
            <button
                type="button"
                onClick={handleClick}
                disabled={isDisabled}
                className="date-button"
            >
                {date.getDate()}
            </button>
        </td>
    );
};

CalendarCell.propTypes = {
    date: PropTypes.instanceOf(Date),
    isDisabled: PropTypes.bool,
    isSelected: PropTypes.bool,
    isPast: PropTypes.bool,
    isSubmitted: PropTypes.bool,
    onClick: PropTypes.func.isRequired
};

CalendarCell.defaultProps = {
    date: null,
    isDisabled: false,
    isSelected: false,
    isPast: false,
    isSubmitted: false
};

export default CalendarCell; 