import React from 'react';
import PropTypes from 'prop-types';

const CalendarCell = ({
    day,
    date,
    isSelected,
    isDisabled,
    isPast,
    isSubmitted,
    onClick
}) => {
    const getCellClasses = () => {
        const classes = ['calendar-cell'];
        if (isSelected) classes.push('selected');
        if (isDisabled) classes.push('disabled');
        if (isPast) classes.push('past');
        if (isSubmitted) classes.push('submitted');
        return classes.join(' ');
    };

    return (
        <button
            className={getCellClasses()}
            onClick={() => !isDisabled && !isPast && !isSubmitted && onClick(date)}
            disabled={isDisabled || isPast || isSubmitted}
            type="button"
        >
            {day}
        </button>
    );
};

CalendarCell.propTypes = {
    day: PropTypes.number.isRequired,
    date: PropTypes.string.isRequired,
    isSelected: PropTypes.bool,
    isDisabled: PropTypes.bool,
    isPast: PropTypes.bool,
    isSubmitted: PropTypes.bool,
    onClick: PropTypes.func.isRequired
};

CalendarCell.defaultProps = {
    isSelected: false,
    isDisabled: false,
    isPast: false,
    isSubmitted: false
};

export default CalendarCell; 