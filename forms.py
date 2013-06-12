import re
import bitcoin_validation as bcv
import wtforms as wtf
from flask.ext.wtf import Form
from wtforms import validators


class InformationForm(Form):
    email = wtf.TextField(u'Email address',
        validators = [wtf.validators.InputRequired(), wtf.validators.Email()])
    username = wtf.TextField(u'Forum username',
        validators = [wtf.validators.InputRequired()])
    refund_address = wtf.TextField(u'Bitcoin address for refunds',
        validators = [wtf.validators.InputRequired()])

    def validate_refund_address(form, field):        
        if not bcv.valid_address(field.data):
            raise wtf.ValidationError("Invalid Bitcoin address!")
            
        return True

class MinerForm(Form):
    k1s = wtf.IntegerField(u'Number of K1s desired', validators = [
        wtf.validators.InputRequired(), wtf.validators.NumberRange(min=0)])
    k16s = wtf.IntegerField(u'Number of K16s desired', validators = [
        wtf.validators.InputRequired(), wtf.validators.NumberRange(min=0)])
    k64s = wtf.IntegerField(u'Number of K64s desired', validators = [
        wtf.validators.InputRequired(), wtf.validators.NumberRange(min=0)])
    k16substitution = wtf.BooleanField(u'Substitute K16s for my requested K64s if not enough K64s are ordered from my group buy.')
    bump = wtf.BooleanField(u'If my group buy doesn\'t generate enough orders, bump me to a later group buy instead of refunding me.')


class GroupBuyForm(Form):
    organizer = wtf.TextField(u'Organizer username',
        validators = [wtf.validators.InputRequired()])
    batch = wtf.IntegerField(u'Batch number',
        validators = [wtf.validators.NumberRange(min=1)])
    chips = wtf.IntegerField(u'Number of chips',
        validators = [wtf.validators.NumberRange(min=1)])


class OrderForm(Form):
    information = wtf.FormField(InformationForm)
    miners = wtf.FormField(MinerForm)
    group_buys = wtf.FieldList(wtf.FormField(GroupBuyForm), min_entries = 1)

    def validate(self):
        valid = super(OrderForm, self).validate()
        chip_supply_difference = self.chip_supply_difference()

        if chip_supply_difference > 0:
            valid = False
            self.errors['chip_supply_error'] = ("Not enough chips in your "
            + "group buys for the number of miners you've requested!")
        elif chip_supply_difference < 0:
            valid = False
            self.errors['chip_supply_error'] = ("Too many chips in your "
            + " group buys for the number of miners you've requested!")

        return valid

    def chip_supply_difference(form):
        k1s = form.miners.k1s.data or 0;
        k16s = form.miners.k16s.data or 0;
        k64s = form.miners.k64s.data or 0;

        chips_required = k1s + (k16s * 16) + (k64s * 64)
        chips_supplied = sum([(gb_form.chips.data or 0
            ) for gb_form in form.group_buys])
        
        return chips_required - chips_supplied
