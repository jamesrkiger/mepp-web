/*
 * MEPP - A web application to guide patients and clinicians in the process of
 * facial palsy rehabilitation, with the help of the mirror effect and principles
 * of motor learning
 * Copyright (C) 2021 MEPP <info@mirroreffectplus.org>
 *
 * This file is part of MEPP.
 *
 * MEPP is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * MEPP is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with MEPP.  If not, see <http://www.gnu.org/licenses/>.
 */
import React, { useEffect, useState } from 'react';
import {
  ArrayInput,
  BooleanInput,
  Edit,
  NumberInput,
  ReferenceField,
  SelectInput,
  SimpleForm,
  SimpleFormIterator,
  TextField,
  TextInput,
  TranslatableInputs,
  useGetList,
  useLocale,
  usePermissions,
  useTranslate,
} from 'react-admin';

import SubCategoryInput from '@components/admin/exercises/SubCategoryInput';
import { preSave } from '@components/admin/exercises/callbacks';
import {
  useNumberStyles,
  useSimpleFormIteratorStyles,
  useTranslatorInputStyles,
} from '@components/admin/exercises/styles';
import {
  validateCategory,
  validateSubCategory,
  validateSubCategories,
} from '@components/admin/exercises/validators';
import { Typography, Div } from '@components/admin/shared/dom/sanitize';
import SimpleFormToolBar from '@components/admin/shared/toolbars/SimpleFormToolbar';
import TopToolbar from '@components/admin/shared/toolbars/TopToolbar';
import { validateNumber } from '@components/admin/shared/validators';
import { requiredLocalizedField } from '@components/admin/shared/validators';

import { LANGUAGES } from '../../../locales';

export const ExerciseEdit = (props) => {
  const t = useTranslate();
  const { permissions } = usePermissions() 
  const simpleFormIteratorclasses = useSimpleFormIteratorStyles();
  const numberClasses = useNumberStyles();
  const translatorClasses = useTranslatorInputStyles();
  const locale = useLocale();
  const [updatedSubCategoryInputs, setUpdatedSubCategoryInputs] = useState({});
  let categories = [];
  let subCategories = {};
  const { data, isLoading } = useGetList(
    'categories',
    {
      pagination: { page: 1, perPage: 9999 },
      sort: { field: 'i18n__name', order: 'ASC' },
    },
    { language: locale },
  );

  const validateI18n = (record) => {
    return requiredLocalizedField(record, locale, 'description');
  };
  /* Update description translations if empty */
  const transform = (record) => {
    return preSave(record, locale);
  };

  /* Populate dynamically subcategories */
  const handleChange = (event) => {
    const categoryInput = event.target;
    const updates = {};

    updates[categoryInput.name.replace('category__', '')] = categoryInput.value;
    setUpdatedSubCategoryInputs({
      ...updatedSubCategoryInputs,
      ...updates,
    });
  };
  // ToDo refactor
  if (!isLoading) {
    data.forEach((category) => {
      categories.push({
        'id': category.id,
        'name': category.i18n.name[locale],
      });
      subCategories[category.id] = category.sub_categories.map(
        (subCategory) => {
          return {
            'id': subCategory.id,
            'name': subCategory.i18n.name[locale],
          };
        },
      );
    });
  }

  return (
    <Edit
      transform={transform}
      undoable={false}
      actions={<TopToolbar />}
      {...props}
    >
      <SimpleForm
        toolbar={<SimpleFormToolBar identity={false} />}
        validate={validateI18n}
      >
        <Typography variant="h6" gutterBottom>
          {t('resources.exercises.card.labels.definition')}
        </Typography>
        {permissions === 'admin' && (
          <ReferenceField
            source="clinician_uid"
            reference="clinicians"
            link="show"
          >
            <TextField source="full_name" />
          </ReferenceField>
        )}
        <TranslatableInputs
          locales={LANGUAGES}
          defaultLocale={locale}
          classes={translatorClasses}
        >
          <TextInput
            source="i18n.description"
            multiline={true}
            fullWidth={true}
          />
        </TranslatableInputs>
        {permissions === 'admin' && <BooleanInput source="is_system" />}
        <Div className={numberClasses.numbers}>
          <NumberInput
            source="movement_duration"
            validate={validateNumber}
            label={t('resources.exercises.fields.movement_duration')}
          />
          <NumberInput
            source="pause"
            validate={validateNumber}
            label={t('resources.exercises.fields.pause')}
          />
          <NumberInput
            source="repeat"
            validate={validateNumber}
            label={t('resources.exercises.fields.repeat')}
          />
        </Div>
        <Typography variant="h6" gutterBottom gutterTop={true}>
          {t('resources.exercises.card.labels.classification')}
        </Typography>
        {!isLoading && (
          <ArrayInput
            source="sub_categories"
            validate={validateSubCategories}
            fullWidth={false}
          >
            <SimpleFormIterator
              classes={simpleFormIteratorclasses}
              disableReordering={true}
            >
              <SelectInput
                source="category__uid"
                choices={categories}
                onChange={handleChange}
                validate={validateCategory}
              />
              <SubCategoryInput
                source="uid"
                updatedSubCategoryInputs={updatedSubCategoryInputs}
                subCategories={subCategories}
                validate={validateSubCategory}
              />
            </SimpleFormIterator>
          </ArrayInput>
        )}
      </SimpleForm>
    </Edit>
  );
};
